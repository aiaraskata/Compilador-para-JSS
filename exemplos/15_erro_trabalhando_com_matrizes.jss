function int somaMatriz(int[] matriz) {
    return matriz[0][0];
}

function int somaVetor(int[] vetor) {
    return vetor[0];
}

function int somaEscalar(int x) {
    return x;
}

function void main() {
    let int [3][3] matriz;
    let int [3] vetor;
    let int x;

    somaMatriz(matriz);
    somaVetor(vetor);
    somaEscalar(x);
}