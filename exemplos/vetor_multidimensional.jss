function int somarDiagonal(int[][] matriz) {
    return matriz[0][0] + matriz[1][1];
}

function void main() {
    let int [2][2] matriz = [[1, 2], [3, 4]];
    let real [2][2][2] cubo;

    matriz[0][1] = 10;
    cubo[1][0][1] = 3.5;

    console.log(somarDiagonal(matriz));
}
