//first function start
window.addEventListener('scroll', function() {
    var tableHeader = document.querySelector('thead');
    var rect = tableHeader.getBoundingClientRect();
    
    if (rect.top <= 0) {
        tableHeader.classList.add('sticky');
    } else {
        tableHeader.classList.remove('sticky');
    }
});//first function end


// 1-20, -1 -20 color border function start
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
});// 1-20, -1 -20 color border function end

//arrow key function start
window.addEventListener('DOMContentLoaded', function() {
    var arrowKey = document.getElementById('arrow-key');
    var greenCells = document.querySelectorAll('td.highlight-green');
    var redCells = document.querySelectorAll('td.highlight-red');

    var currentIndex = -1;
    var clickCount = 0;

    arrowKey.addEventListener('click', function() {
        clickCount++;

        if (clickCount === 1) {
            if (currentIndex === -1 || currentIndex === greenCells.length - 1) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }

            if (greenCells.length > 0) {
                greenCells.forEach(function(cell) {
                    cell.classList.remove('current');
                });

                greenCells[currentIndex].classList.add('current');
                greenCells[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else if (clickCount === 2) {
            if (currentIndex === -1 || currentIndex === redCells.length - 1) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }

            if (redCells.length > 0) {
                redCells.forEach(function(cell) {
                    cell.classList.remove('current');
                });

                redCells[currentIndex].classList.add('current');
                redCells[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            clickCount = 0;
        }
    });
});// arrow key function end

//selection function start
document.addEventListener('DOMContentLoaded', function() {
    var cells = document.querySelectorAll('td, th');
    var rows = document.querySelectorAll('tr');
    var isArtMode = false;
    var selectedColor = '#ff0000';

    // Add event listeners to cells and rows
    cells.forEach(function(cell) {
        cell.addEventListener('click', handleCellClick);
    });

    rows.forEach(function(row) {
        row.addEventListener('click', handleRowClick);
    });

    // Handle cell click event
    function handleCellClick(event) {
        if (isArtMode) {
            event.target.style.backgroundColor = selectedColor;
        } else {
            event.target.classList.toggle('highlighted');
        }
    }

    // Handle row click event
    function handleRowClick(event) {
        if (isArtMode) {
            var cells = event.currentTarget.querySelectorAll('td, th');
            cells.forEach(function(cell) {
                cell.style.backgroundColor = selectedColor;
            });
        } else {
            event.currentTarget.classList.toggle('highlighted');
        }
    }

    // Handle color picker change event
    var colorPicker = document.getElementById('selected-color');
    colorPicker.addEventListener('input', function(event) {
        selectedColor = event.target.value;
    });

    // Toggle art mode
    var colorPickerDiv = document.getElementById('color-picker');
    colorPickerDiv.addEventListener('click', function() {
        isArtMode = !isArtMode;
        colorPickerDiv.classList.toggle('art-mode');
    });
});//selection function end

//art function start
// Variables to track the selected color and mode
let selectedColor = '';
let mode = 'select';

// Add click event listener to the dot element
const dotElement = document.querySelector('#dot');
dotElement.addEventListener('click', toggleMode);

// Function to toggle between select and art mode
function toggleMode() {
  if (mode === 'select') {
    mode = 'art';
    dotElement.style.backgroundColor = selectedColor;
    document.addEventListener('click', handleArtClick);
  } else {
    mode = 'select';
    dotElement.style.backgroundColor = 'black';
    document.removeEventListener('click', handleArtClick);
  }
}

// Function to handle click events when in art mode
function handleArtClick(event) {
  const clickedElement = event.target;
  if (clickedElement !== dotElement) {
    clickedElement.style.backgroundColor = selectedColor;
  }
}

// Add click event listeners to cells and rows for selecting
const cells = document.querySelectorAll('td');
const rows = document.querySelectorAll('tr');

cells.forEach((cell) => {
  cell.addEventListener('click', handleCellClick);
});

rows.forEach((row) => {
  row.addEventListener('click', handleRowClick);
});

// Function to handle click events on cells
function handleCellClick(event) {
  const cell = event.target;
  cell.style.backgroundColor = selectedColor;
}

// Function to handle click events on rows
function handleRowClick(event) {
  const row = event.target;
  const cellsInRow = row.querySelectorAll('td');
  cellsInRow.forEach((cell) => {
    cell.style.backgroundColor = selectedColor;
  });
}

// Function to set the selected color
function setColor(color) {
  selectedColor = color;
}
