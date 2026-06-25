function void main() {
    let int contador = 5;
    let str texto = "validar";

    // ERRO 1: Condição do IF deve ser bool, obtido int
    if (contador) {
        console.log("Falha");
    }

    // ERRO 2: Condição do WHILE deve ser bool, obtido str
    while (texto) {
        console.log("Loop infinito inválido");
    }
}