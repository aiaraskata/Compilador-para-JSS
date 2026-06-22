class Ponto {
    int x;
    int y;

    Ponto constructor(int x, int y) {
        this.x = x;
        this.y = y;
    }

    int soma() {
        return this.x + this.y;
    }
}

function int fatorial(int n) {
    if (n > 1) {
        return n * fatorial(n - 1);
    } else {
        return 1;
    }
}

function void main() {
    let int numero;
    let int a, b, c;
    let int [3] valores = [1, 2, 3];
    const Ponto ponto = new Ponto(10, 20);

    input(numero);

    for (let int i = 0; i < 3; ++i) {
        valores[i] += 1;
    }

    console.log("Fatorial:", fatorial(numero));
    console.log("Soma:", ponto.soma());
}
