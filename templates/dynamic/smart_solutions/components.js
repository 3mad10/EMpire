import { subSystems, SOLNLIMIT, SOLNINITIALOFFSET } from './config.js';
import {subsystemListOnHoverEvent, subsystemListOnMouseLeave} from './vidEventHandlers.js'


function createSystemShort(trailer, backgroundImage) {
    // Create video element
    const subSystemShort = document.createElement('div');
    subSystemShort.setAttribute("class", "system-shorts");

    const video = document.createElement('video');
    video.setAttribute("loop", "");
    video.setAttribute("muted", "");
    video.muted = true;
    video.setAttribute("preload", "auto");

    // Create and append source element
    const source = document.createElement('source');
    source.setAttribute('src', trailer); // set your path
    source.setAttribute('type', 'video/mp4');
    video.appendChild(source);

    // Add listener for entering video element area
    subSystemShort.addEventListener('mouseenter', () => {
    source.setAttribute('src', trailer);
    video.load();
    video.play();
    video.style.opacity = 0.7;
    subSystemShort.style.backgroundImage = 'none';
    });

    // Add listener for leaving video element area
    subSystemShort.addEventListener('mouseleave', () => {
    video.pause();
    subSystemShort.style.backgroundImage = `url(${backgroundImage})`;
    video.style.opacity = 0;
    });

    subSystemShort.appendChild(video);

    return subSystemShort;
}


function createSystemSubElements(subElements, videoContainerElement, defaultVideoSrc, backgroundImage) {
    // Create list element
    const elementsList = document.createElement('ul');
    elementsList.setAttribute('class', 'hero-list');

    // Create each element in list
    subElements.forEach(element => {
    const listElement = document.createElement('li');
    const anchorElement = document.createElement('a');
    anchorElement.textContent = element.name;
    anchorElement.setAttribute("href", element.link);
    anchorElement.setAttribute("data-video", element.short);
    listElement.appendChild(anchorElement);
    elementsList.appendChild(listElement);
    });

    elementsList.addEventListener('mouseover', (e) => {
    subsystemListOnHoverEvent(e, videoContainerElement, elementsList);
    });

    elementsList.addEventListener('mouseleave', () => {
    subsystemListOnMouseLeave(videoContainerElement, defaultVideoSrc, backgroundImage);
    });

    return elementsList;
}


export function createSubSystems(subSystems, width) {
    const systemsDiv = document.querySelector('#systems');
    systemsDiv.innerHTML = '';
      
    for (const system of subSystems) {
    // Create container div
    const subSystemDiv = document.createElement('div');
    subSystemDiv.setAttribute("id", system.name);
    subSystemDiv.setAttribute("class", "sub-system");

    // Create system shorts video
    const shortsVideoElement = createSystemShort(system.trailer, system.backgroundImage);

    // Create list of elements inside subsystem
    const subElementsList = createSystemSubElements(system.subElements, shortsVideoElement, system.trailer, system.backgroundImage);

    // Conditionally append: list first for left side, video first for right side
    if (system.position.x < width / 2) {
        subSystemDiv.appendChild(subElementsList);   // List first
        subSystemDiv.appendChild(shortsVideoElement); // Then video
    } else {
        subSystemDiv.appendChild(shortsVideoElement); // Video first
        subSystemDiv.appendChild(subElementsList);   // Then list
    }

    systemsDiv.appendChild(subSystemDiv);

    const div = document.querySelector(`#${system.name}`);
    if (system.position.x < width / 2) {
        const divWidth = div.offsetWidth;
        div.style.left = `${system.position.x - divWidth}px`;
    } else {
        div.style.left = `${system.position.x}px`;
    }
    div.style.top = `${system.position.y}px`;
    }
}


export function createMainLines(circuitLines) {

    const svg = document.getElementById("circuitSvg");
    circuitLines.forEach(LineConfig => {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "path");
        line.setAttribute("d", `M ${LineConfig.startX} ${LineConfig.startY} L ${LineConfig.startX + LineConfig.movementsXOffsets[0]} ${LineConfig.startY + LineConfig.movementsYOffsets[0]} l ${LineConfig.movementsXOffsets[1]} ${LineConfig.movementsYOffsets[1]} l ${LineConfig.movementsXOffsets[2]} ${LineConfig.movementsYOffsets[2]}`)
        line.setAttribute("stroke", "#0ff");
        line.setAttribute("stroke-width", "2");
        line.setAttribute("fill", "None");
        line.setAttribute("filter", "url(#glow)");
        svg.appendChild(line);
    });
}



export function drawCircuit(svg, mainCircutLines) {
      const SVG_NS = "http://www.w3.org/2000/svg";
      svg.innerHTML = `<defs>
                        <filter id="glow">
                          <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#0ff" />
                          <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#0ff" />
                        </filter>
                      </defs>`; // clear lines but keep defs

      // Get width, height and calculate needed size and coordinates
      const width = svg.clientWidth;
      const height = svg.clientHeight;
      const rectSize = svg.clientWidth / 8;
      const centerX = width / 2;
      const centerY = height / 2;

      // Create rectangle according to the window/svg size
      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", centerX - rectSize / 2);
      rect.setAttribute("y", centerY - rectSize / 2);
      rect.setAttribute("width", rectSize);
      rect.setAttribute("height", rectSize);
      rect.setAttribute("fill", "#00415a");
      rect.setAttribute("filter", "url(#glow)");
      svg.appendChild(rect);

      // Create main lines
      createMainLines(mainCircutLines, svg);

      const systems = document.querySelector("#systems");

      subSystems.forEach((val, i) => {
        const LineConfig = mainCircutLines[i];
        const endX = LineConfig.startX + LineConfig.movementsXOffsets[0] + LineConfig.movementsXOffsets[1] + LineConfig.movementsXOffsets[2];
        const endY = LineConfig.startY + LineConfig.movementsYOffsets[0] + LineConfig.movementsYOffsets[1] + LineConfig.movementsYOffsets[2];
        console.log(`SUBSYSTEM ${i}`)
        console.log(`endX : ${endX}`)
        console.log(`endY : ${endY}`)

        if (endX < width/2) {
          console.log(`position left endX = ${endX}`)
          subSystems[i].position = {x : endX - 0.05 * rectSize, y : endY - Math.abs(LineConfig.movementsYOffsets[1]) / 2};
        } else{
          subSystems[i].position = {x : endX + 0.05 * rectSize, y : endY - Math.abs(LineConfig.movementsYOffsets[1]) / 2};
        }
      });

      // Create vision systems div
      createSubSystems(subSystems, width);

    }
     