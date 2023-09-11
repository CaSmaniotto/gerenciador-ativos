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