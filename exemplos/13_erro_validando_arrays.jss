function void main() {
    let int [3][3] matriz;
    let int i;
    let int j;

    matriz[0][0] = 1;
    matriz[0][1] = 2;
    matriz[0][2] = 3;
    matriz[1][0] = 4;
    matriz[1][1] = 5;
    matriz[1][2] = 6;
    matriz[2][0] = 7;
    matriz[2][1] = 8;
    matriz[2][2] = 9;

    for (let int i = 0; i < 3; ++i) {
        for (let int j = 0; j < 3; ++j) {
            console.log(matriz[x][j]);
        }
    }
}