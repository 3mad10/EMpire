import { subSystems, SOLNLIMIT, SOLNINITIALOFFSET } from './config.js';
import {drawCircuit, createSubSystems, createMainLines} from './components.js';
import {createSystemsSections} from './sections.js';
import {updateScrollLineGradient} from './pageEventListeners.js'

const svg = document.getElementById("circuitSvg");

function getMainCircuitLines() {
    // Get width, height and calculate needed size and coordinates
    const width = svg.clientWidth;
    const height = svg.clientHeight;
    const rectSize = svg.clientWidth / 8; // Or svg.clientHeight / 8 depending on desired aspect
    const centerX = width / 2;
    const centerY = height / 2;

    // Now define mainCircutLines using the calculated values
    const mainCircutLines = [
        // top right
        {
            startX: centerX + rectSize / 2,
            startY: centerY - 0.7 * (rectSize / 2),
            movementsXOffsets: [width / 10, 0, width / 10],
            movementsYOffsets: [0, -width / 10, 0],
        },
        // bottom right
        {
            startX: centerX + rectSize / 2,
            startY: centerY + 0.7 * (rectSize / 2),
            movementsXOffsets: [width / 10, 0, width / 10],
            movementsYOffsets: [0, width / 10, 0],
        },
        // top left
        {
            startX: centerX - rectSize / 2,
            startY: centerY - 0.7 * (rectSize / 2),
            movementsXOffsets: [-width / 10, 0, -width / 10],
            movementsYOffsets: [0, -width / 10, 0],
        },
        {
            startX: centerX - rectSize / 2,
            startY: centerY + 0.7 * (rectSize / 2),
            movementsXOffsets: [-width / 10, 0, -width / 10],
            movementsYOffsets: [0, width / 10, 0],
        }
    ];
    return mainCircutLines;
}

// Ensure the DOM is fully loaded before trying to access elements
document.addEventListener('DOMContentLoaded', () => {

    if (!svg) {
        console.error("SVG element with ID 'circuitSvg' not found.");
        return; // Exit if the element isn't there
    }

    const systemsSection = document.getElementById("content");
    createSystemsSections(systemsSection);

    const heroSection = document.getElementById("hero");
    const imprintedDivLeft = document.createElement("div");
    imprintedDivLeft.innerText = "AI Solutions"
    imprintedDivLeft.setAttribute("class", "imprinted-text imprinted-left");
    heroSection.appendChild(imprintedDivLeft);

    const imprintedDivRight = document.createElement("div");
    imprintedDivRight.innerText = "For Everything"
    imprintedDivRight.setAttribute("class", "imprinted-text imprinted-right");
    heroSection.appendChild(imprintedDivRight);
    
    const mainCircutLines = getMainCircuitLines();
    drawCircuit(svg, mainCircutLines);

    

    window.addEventListener("resize", () => {
        const mainCircutLines = getMainCircuitLines();
        drawCircuit(svg, mainCircutLines)
    });

    window.addEventListener('scroll', updateScrollLineGradient);
    window.addEventListener('resize', updateScrollLineGradient);
    window.addEventListener('DOMContentLoaded', updateScrollLineGradient);
});


