function void main() {
    let int valorInteiro = 10;
    let real valorReal = 4.5;
    
    // Promoção implícita: int + real resulta em real
    let real resultadoSoma = valorInteiro + valorReal;

    let str textoBase = "O resultado da soma é: ";
    
    // Concatenação: str + real resulta em str
    let str mensagemFinal = textoBase + resultadoSoma;

    console.log(mensagemFinal);
}