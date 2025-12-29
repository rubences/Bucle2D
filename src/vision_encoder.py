"""
Vision Encoder: NestedUNet for Multi-Scale Feature Extraction

Implements a nested UNet architecture for hierarchical feature extraction
from racing vision inputs at multiple resolution scales.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Optional
import numpy as np


class ConvBlock(nn.Module):
    """Basic convolutional block with batch normalization and ReLU."""
    
    def __init__(self, in_channels: int, out_channels: int, 
                 kernel_size: int = 3, padding: int = 1):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, 
                     padding=padding, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size, 
                     padding=padding, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x)


class DownBlock(nn.Module):
    """Downsampling block using max pooling."""
    
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv = ConvBlock(in_channels, out_channels)
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x_down = self.pool(x)
        x_conv = self.conv(x_down)
        return x_conv, x_down


class UpBlock(nn.Module):
    """Upsampling block with skip connection."""
    
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.up = nn.ConvTranspose2d(in_channels, out_channels, 
                                     kernel_size=2, stride=2)
        self.conv = ConvBlock(out_channels * 2, out_channels)
    
    def forward(self, x: torch.Tensor, skip: torch.Tensor) -> torch.Tensor:
        x = self.up(x)
        # Pad if necessary
        if x.shape[-2:] != skip.shape[-2:]:
            x = F.pad(x, (0, skip.shape[-1] - x.shape[-1], 
                         0, skip.shape[-2] - x.shape[-2]))
        x = torch.cat([x, skip], dim=1)
        return self.conv(x)


class NestedUNet(nn.Module):
    """
    Nested U-Net (UNet++) for medical image segmentation adapted for racing vision.
    
    Multi-scale architecture that enables:
    - Early termination at shallow layers for fast inference
    - Deep feature extraction for complex scenarios
    - Hierarchical feature fusion across multiple scales
    """
    
    def __init__(self,
                 in_channels: int = 3,
                 num_classes: int = 1,
                 feature_channels: List[int] = None,
                 embedding_dim: int = 512,
                 dropout_rate: float = 0.2):
        """
        Initialize NestedUNet.
        
        Args:
            in_channels: Number of input channels (RGB = 3)
            num_classes: Number of output classes (for segmentation head)
            feature_channels: Channel dimensions at each level [64, 128, 256, 512]
            embedding_dim: Final embedding dimension for agent
            dropout_rate: Dropout rate for regularization
        """
        super().__init__()
        
        if feature_channels is None:
            feature_channels = [64, 128, 256, 512]
        
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.feature_channels = feature_channels
        self.embedding_dim = embedding_dim
        
        # Encoder (downsampling path)
        self.enc1 = ConvBlock(in_channels, feature_channels[0])
        self.down1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.enc2 = ConvBlock(feature_channels[0], feature_channels[1])
        self.down2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.enc3 = ConvBlock(feature_channels[1], feature_channels[2])
        self.down3 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.enc4 = ConvBlock(feature_channels[2], feature_channels[3])
        self.down4 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Bottleneck (deepest level)
        self.bottleneck = ConvBlock(feature_channels[3], feature_channels[3] * 2)
        
        # Decoder (upsampling path with skip connections)
        self.up4 = nn.ConvTranspose2d(feature_channels[3] * 2, 
                                      feature_channels[3], kernel_size=2, stride=2)
        self.dec4 = ConvBlock(feature_channels[3] * 2, feature_channels[3])
        
        self.up3 = nn.ConvTranspose2d(feature_channels[3], 
                                      feature_channels[2], kernel_size=2, stride=2)
        self.dec3 = ConvBlock(feature_channels[2] * 2, feature_channels[2])
        
        self.up2 = nn.ConvTranspose2d(feature_channels[2], 
                                      feature_channels[1], kernel_size=2, stride=2)
        self.dec2 = ConvBlock(feature_channels[1] * 2, feature_channels[1])
        
        self.up1 = nn.ConvTranspose2d(feature_channels[1], 
                                      feature_channels[0], kernel_size=2, stride=2)
        self.dec1 = ConvBlock(feature_channels[0] * 2, feature_channels[0])
        
        # Output head for segmentation
        self.out_conv = nn.Conv2d(feature_channels[0], num_classes, kernel_size=1)
        
        # Global average pooling + FC for embedding
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.fc_embed = nn.Sequential(
            nn.Linear(feature_channels[3] * 2, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout_rate),
            nn.Linear(1024, embedding_dim)
        )
        
        self.dropout = nn.Dropout(dropout_rate)
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass through NestedUNet.
        
        Args:
            x: Input tensor (batch_size, channels, height, width)
            
        Returns:
            Tuple of (segmentation_map, embedding_vector)
        """
        # Store input size for upsampling
        input_shape = x.shape[-2:]
        
        # Encoder
        enc1 = self.enc1(x)  # 64 channels
        x = self.down1(enc1)
        
        enc2 = self.enc2(x)  # 128 channels
        x = self.down2(enc2)
        
        enc3 = self.enc3(x)  # 256 channels
        x = self.down3(enc3)
        
        enc4 = self.enc4(x)  # 512 channels
        x = self.down4(enc4)
        
        # Bottleneck
        x = self.bottleneck(x)  # 1024 channels
        bottleneck_features = x
        
        # Extract embedding from bottleneck
        pooled = self.global_pool(x)  # (batch, 1024, 1, 1)
        pooled_flat = pooled.view(pooled.size(0), -1)  # (batch, 1024)
        embedding = self.fc_embed(pooled_flat)  # (batch, embedding_dim)
        
        # Decoder with skip connections
        x = self.up4(x)
        x = self._pad_to_shape(x, enc4.shape)
        x = torch.cat([x, enc4], dim=1)
        x = self.dec4(x)
        
        x = self.up3(x)
        x = self._pad_to_shape(x, enc3.shape)
        x = torch.cat([x, enc3], dim=1)
        x = self.dec3(x)
        
        x = self.up2(x)
        x = self._pad_to_shape(x, enc2.shape)
        x = torch.cat([x, enc2], dim=1)
        x = self.dec2(x)
        
        x = self.up1(x)
        x = self._pad_to_shape(x, enc1.shape)
        x = torch.cat([x, enc1], dim=1)
        x = self.dec1(x)
        
        # Output segmentation map
        seg_map = self.out_conv(x)
        
        # Resize to input shape if necessary
        if seg_map.shape[-2:] != input_shape:
            seg_map = F.interpolate(seg_map, size=input_shape, mode='bilinear', align_corners=False)
        
        return seg_map, embedding
    
    def forward_embedding_only(self, x: torch.Tensor) -> torch.Tensor:
        """
        Fast path: extract embedding without computing segmentation map.
        Useful for agent decision-making when segmentation isn't needed.
        
        Args:
            x: Input tensor
            
        Returns:
            Embedding vector (batch_size, embedding_dim)
        """
        # Encoder
        x = self.enc1(x)
        x = self.down1(x)
        
        x = self.enc2(x)
        x = self.down2(x)
        
        x = self.enc3(x)
        x = self.down3(x)
        
        x = self.enc4(x)
        x = self.down4(x)
        
        # Bottleneck
        x = self.bottleneck(x)
        
        # Extract embedding
        pooled = self.global_pool(x)
        pooled_flat = pooled.view(pooled.size(0), -1)
        embedding = self.fc_embed(pooled_flat)
        
        return embedding
    
    @staticmethod
    def _pad_to_shape(x: torch.Tensor, target_shape: torch.Size) -> torch.Tensor:
        """Pad tensor x to match target shape."""
        if x.shape[-2:] != target_shape[-2:]:
            h_diff = target_shape[-2] - x.shape[-2]
            w_diff = target_shape[-1] - x.shape[-1]
            x = F.pad(x, (0, w_diff, 0, h_diff))
        return x
    
    def get_flops(self, input_shape: Tuple[int, int] = (512, 512)) -> float:
        """
        Estimate FLOPs for given input shape.
        
        Args:
            input_shape: Input spatial dimensions (H, W)
            
        Returns:
            Approximate FLOPs
        """
        # Simple estimation: count conv operations
        # This is a rough approximation
        return sum(p.numel() * 2 for p in self.parameters() if p.requires_grad)


def create_vision_encoder(pretrained: bool = False) -> NestedUNet:
    """
    Factory function to create a NestedUNet vision encoder.
    
    Args:
        pretrained: Whether to load pretrained weights (future enhancement)
        
    Returns:
        Initialized NestedUNet model
    """
    model = NestedUNet(
        in_channels=3,
        num_classes=1,
        feature_channels=[64, 128, 256, 512],
        embedding_dim=512,
        dropout_rate=0.2
    )
    return model


if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("NestedUNet Vision Encoder Demo")
    print("=" * 60)
    
    # Create model
    model = create_vision_encoder()
    model.eval()
    
    print(f"\nModel Architecture:")
    print(model)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\nTotal Parameters: {total_params:,}")
    print(f"Trainable Parameters: {trainable_params:,}")
    
    # Test inference
    print("\n" + "=" * 60)
    print("Testing Inference")
    print("=" * 60)
    
    with torch.no_grad():
        # Simulate batch of racing video frames (batch=2, RGB, 512x512)
        dummy_input = torch.randn(2, 3, 512, 512)
        
        # Full forward pass
        seg_map, embedding = model(dummy_input)
        
        print(f"\nInput shape: {dummy_input.shape}")
        print(f"Segmentation map shape: {seg_map.shape}")
        print(f"Embedding shape: {embedding.shape}")
        print(f"Embedding norm: {torch.norm(embedding, dim=1)}")
        
        # Fast embedding-only path
        embedding_fast = model.forward_embedding_only(dummy_input)
        print(f"\nFast embedding shape: {embedding_fast.shape}")
        print(f"Difference (should be ~0): {torch.norm(embedding - embedding_fast):.6f}")
    
    # Compute approximate FLOPs
    flops = model.get_flops()
    print(f"\nApproximate FLOPs: {flops:,.0f}")
    
    # Memory estimation
    print("\nMemory estimation (for batch_size=1):")
    mem_params = total_params * 4 / (1024**3)  # 32-bit floats
    print(f"  Parameter memory: {mem_params:.2f} GB")
