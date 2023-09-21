// table filter
$(document).ready(function(){
    $("#input").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#table tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

const changeSize = () => {
    const elements = document.querySelectorAll('*');
    // console.log(this)

    elements.forEach(element => {
        // const computedStyle = window.getComputedStyle(element);
        // const fontSize = parseFloat(computedStyle.fontSize);

        // element.style.fontSize = fontSize * 1.1 + 'px';
        // console.log(element.style.fontSize)
        element.classList.toggle('changeFont');
    });

    // Verifica se a classe de fonte foi ativada e armazena o estado no localStorage
    const isFontChanged = elements[0].classList.contains('changeFont');
    localStorage.setItem('fontChanged', isFontChanged);
}

// $(document).ready(function(){
//     $('#btnContraste').click(function(){
//         var element = document.body;
//         element.classList.toggle("dark"); 
        
//         const darkMode = element[0].classList.contains('changeFont');
//         localStorage.setItem('darkMode', darkMode);
//     });
// });   

function toggleDarkMode() {
    var element = document.body;
    element.classList.toggle("dark"); 
    
    const darkMode = element.classList.contains('dark');
    localStorage.setItem('darkMode', darkMode);
}

// Obtém o estado da classe de fonte do localStorage ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    const fontChanged = localStorage.getItem('fontChanged');
    const darkMode = localStorage.getItem('darkMode');

    if (fontChanged === 'true') {
        changeSize();
    }

    if (darkMode === 'true') {
        toggleDarkMode()
    }

});

//timeout alerta
setTimeout(function () {
    document.getElementById("alerta").style.visibility = "hidden";
    document.getElementById("error").style.visibility = "hidden";
}, 4000);

setTimeout(function(){ 
    document.getElementById("alerta").style.opacity='0';
    document.getElementById("error").style.opacity='0';
}, 1000);

//fechar alerta
// function Fechar(){
//     document.getElementById("alerta").style.visibility = "hidden";
// }

document.addEventListener("DOMContentLoaded", function () {
    var tabela = document.getElementById("minhaTabela");
    var mostrarMaisBotao = document.getElementById("mostrarMais");
    var linhasVisiveis = 20; // Defina o número de linhas visíveis que você deseja mostrar inicialmente
    var linhas = tabela.rows;

    // Função para ocultar linhas que não estão dentro do limite visível
    function ocultarLinhas() {
        for (var i = linhasVisiveis; i < linhas.length; i++) {
            linhas[i].style.display = "none";
        }
    }

    ocultarLinhas(); // Oculta linhas iniciais que não estão visíveis

    // Função para mostrar mais linhas quando o botão "Mostrar Mais" for clicado
    mostrarMaisBotao.addEventListener("click", function () {
        for (var i = linhasVisiveis; i < linhasVisiveis + 20 && i < linhas.length; i++) {
            linhas[i].style.display = "table-row";
        }
      linhasVisiveis += 20; // Aumente este valor para mostrar mais ou menos linhas a cada clique
        if (linhasVisiveis >= linhas.length) {
            mostrarMaisBotao.style.display = "none"; // Oculta o botão quando todas as linhas estiverem visíveis
        }
    });

    // Verifica se todas as linhas já estão visíveis e oculta o botão
    if (linhasVisiveis >= linhas.length) {
        mostrarMaisBotao.style.display = "none";
    }
});