class Main {
  public static void main(String[] args) {
    final int NUM_FILAS = 2;  
    final int NUM_COLUMNAS = 3;  
    char[][] tab2d = new char[NUM_FILAS][NUM_COLUMNAS];          tab2d[0][0] = 'E';  
         tab2d[0][1] = 'N';  
         tab2d[0][2] = 'I';  
         tab2d[1][0] = 'D';  
         tab2d[1][1] = 'e';  
         tab2d[1][2] = 'v';  
    for(int j=0; j<tab2d.length; j++) {  
      for(int i=0; i<tab2d[j].length; i++) {  
          System.out.print(tab2d[j][i]);  
      }  
      System.out.println();  
    } 
  }
}