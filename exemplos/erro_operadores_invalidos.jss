function void main() {
    let int[2] listaA = [1, 2];
    let int[2] listaB = [3, 4];
    let real base = 2.5;

    // ERRO 1: Operadores relacionais (>, <, >=, <=) não se aplicam a vetores
    let bool teste = listaA > listaB;

    // ERRO 2: Operador de potência (**) exige operandos estritamente inteiros
    let int calculo = base ** 3;
}