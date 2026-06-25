class Ponto {
    int x;
    int y;

    Ponto constructor(int x, int y) {
        this.x = x;
        this.y = y;
    }

    int soma() {
        return this.x;
    }
}

function int fatorial(int n) {
    if (n > 1) {
        return n;
    } else {
        return 1;
    }
}

function int maximo(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

function void imprimirResultado(int valor) {
    console.log(valor);
}

function void main() {
    let int a;
    let int b;
    let int resultado;
    const Ponto p = new Ponto(10, 20);

    input(a, b);

    resultado = fatorial(5);
    resultado = maximo(a, b);
    imprimirResultado(resultado);

    for (let int i = 0; i < 10; ++i) {
        resultado = maximo(i, resultado);
    }

    console.log("Maximo:", resultado);
}