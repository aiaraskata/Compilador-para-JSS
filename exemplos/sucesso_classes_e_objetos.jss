class Retangulo {
    int largura;
    int altura;

    Retangulo constructor(int largura, int altura) {
        this.largura = largura;
        this.altura = altura;
    }

    int calcularArea() {
        return this.largura * this.altura;
    }
}

function void main() {
    // Instanciação correta de objeto de classe usando 'new'
    let Retangulo meuRetangulo = new Retangulo(5, 10);
    
    // Acesso e atribuição de atributos de objeto
    meuRetangulo.largura = 6;

    // Chamada de método de objeto e captura de retorno
    let int area = meuRetangulo.calcularArea();
    
    console.log("Area do retangulo: ");
    console.log(area);
}