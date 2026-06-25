function real calcularDesconto(real valorTotal, int percentagem) {
    let real taxa = real(percentagem) / 100.0;
    return valorTotal * taxa;
}

function void main() {
    let int precoBase = 250;
    let int descontoFixo = 15;

    // CORREÇÃO: Adicionado 'let' antes da declaração
    let real economia = calcularDesconto(real(precoBase), descontoFixo);

    // Casting do resultado real para string para fins de exibição
    let str resultadoTexto = "Desconto obtido: " + str(economia);
    
    console.log(resultadoTexto);
}