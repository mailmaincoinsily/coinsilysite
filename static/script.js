window.addEventListener('scroll', function() {
    var tableHeader = document.querySelector('thead');
    var rect = tableHeader.getBoundingClientRect();
    
    if (rect.top <= 0) {
        tableHeader.classList.add('sticky');
    } else {
        tableHeader.classList.remove('sticky');
    }
});

window.addEventListener('DOMContentLoaded', function() {
    var arbitrageCells = document.querySelectorAll('td.arbitrage');

    arbitrageCells.forEach(function(cell) {
        var arbitrage = parseFloat(cell.textContent);
        
        if (arbitrage >= 1 && arbitrage <= 20) {
            cell.classList.add('highlight-green');
        } else if (arbitrage >= -20 && arbitrage <= -1) {
            cell.classList.add('highlight-red');
        }
    });
});

// Add this code inside your script.js file

// Get the arrow key element
var arrowKey = document.getElementById('arrow-key');
var isGreenHighlighted = true;

// Handle click event on arrow key
arrowKey.addEventListener('click', function() {
    // Toggle between green and red highlights
    if (isGreenHighlighted) {
        highlightGreen();
        isGreenHighlighted = false;
    } else {
        highlightRed();
        isGreenHighlighted = true;
    }
});

// Function to highlight green
function highlightGreen() {
    var greenHighlights = document.querySelectorAll('.highlight-green');
    greenHighlights.forEach(function(element) {
        element.classList.remove('highlight-green');
    });
}

// Function to highlight red
function highlightRed() {
    var redHighlights = document.querySelectorAll('.highlight-red');
    redHighlights.forEach(function(element) {
        element.classList.remove('highlight-red');
    });
}

