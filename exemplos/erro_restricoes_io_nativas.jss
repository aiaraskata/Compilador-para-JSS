class Dado { int valor; Dado constructor() { this.valor = 1; } }

function void main() {
    const int taxa = 15;
    let int[5] idades = [10, 20, 30, 40, 50];
    let Dado d = new Dado();

    // ERRO 1: Input não pode ler para constante
    input(taxa); 

    // ERRO 2: Input não pode ler diretamente para uma estrutura de vetor
    input(idades); 

    // ERRO 3: Console.log não pode imprimir objetos complexos de classes
    console.log(d); 

    // ERRO 4: Console.log não pode imprimir vetores inteiros de uma vez
    console.log(idades); 
}