// ERRO SEMÂNTICO: Tipo de retorno não pode ser vetor (usando [] para o Parser aceitar)
function int[] obterDirecoes() {
    let int[2] d = [1, 2];
    return d;
}

// ERRO SEMÂNTICO: A função main deve ser estritamente sem parâmetros
function void main(int argumentos) {
    let int x = 0;
}