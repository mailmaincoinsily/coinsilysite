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
window.addEventListener('DOMContentLoaded', function() {
    var drawingBoard = document.getElementById('drawing-board');
    var isDrawing = false;
    var selectedColor = '#000';

    // Add mousedown event listener to start drawing or select elements
    drawingBoard.addEventListener('mousedown', handleMouseDown);
    // Add mousemove event listener to draw or select elements
    drawingBoard.addEventListener('mousemove', handleMouseMove);
    // Add mouseup event listener to stop drawing or selecting elements
    drawingBoard.addEventListener('mouseup', handleMouseUp);

    function handleMouseDown(event) {
        // Check if the drawing board is clicked
        if (event.target === drawingBoard) {
            isDrawing = true;
        }
    }

    function handleMouseMove(event) {
        // Check if drawing mode is enabled
        if (isDrawing) {
            var dot = createDot(event.clientX, event.clientY);
            drawingBoard.appendChild(dot);
        }
    }

    function handleMouseUp() {
        isDrawing = false;
    }

    function createDot(x, y) {
        var dot = document.createElement('div');
        dot.className = 'dot';
        dot.style.backgroundColor = selectedColor;
        dot.style.left = x + 'px';
        dot.style.top = y + 'px';
        return dot;
    }

    var colorPicker = document.createElement('div');
    colorPicker.className = 'color-picker';
    colorPicker.addEventListener('click', openColorPalette);
    document.body.appendChild(colorPicker);

    function openColorPalette() {
        var colorPalette = document.createElement('input');
        colorPalette.type = 'color';
        colorPalette.addEventListener('change', function() {
            selectedColor = colorPalette.value;
            colorPicker.style.backgroundColor = selectedColor;
            document.body.removeChild(colorPalette);
        });
        document.body.appendChild(colorPalette);
        colorPalette.click();
    }
});
