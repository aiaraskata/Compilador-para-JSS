class Carro { int ano; Carro constructor() { this.ano = 2026; } }

function void main() {
    const int limite = 100;
    const int[3] grade = [1, 2, 3];
    const Carro c = new Carro();

    // ERRO 1: Tipos incompatíveis (int não recebe str)
    let int score = "nota dez"; 

    // ERRO 2: Modificar variável constante
    limite = 200; 

    // ERRO 3: Modificar índice de vetor constante
    grade[0] = 5; 

    // ERRO 4: Modificar atributo de objeto constante
    c.ano = 2027; 
}