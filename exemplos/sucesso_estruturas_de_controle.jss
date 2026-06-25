function void main() {
    let int limite = 5;
    let int contador = 0;

    while (contador < limite) {
        console.log(contador);
        ++contador; // Formato Pré-fixado correto
    }

    for (let int i = 0; i < 3; ++i) { // Formato Pré-fixado correto
        console.log("Iteracao do for");
    }
}