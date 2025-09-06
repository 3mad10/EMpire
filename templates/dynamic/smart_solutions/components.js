import { subSystems, SOLNLIMIT, SOLNINITIALOFFSET } from './config.js';
import {subsystemListOnHoverEvent, subsystemListOnMouseLeave} from './eventHandlers.js'


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

function generateComlementaryLines() {
  const svg = document.getElementById("circuitSvg");

  // Get width, height and calculate needed size and coordinates
    const width = svg.clientWidth;
    const height = svg.clientHeight;
    const rectSize = svg.clientWidth / 8; // Or svg.clientHeight / 8 depending on desired aspect
    const centerX = width / 2;
    const centerY = height / 2;

    // Now define mainCircutLines using the calculated values
    const rightLines = [
        // Right between main up and horizontal
        {
            startX: centerX + rectSize / 2,
            startY: centerY - 0.4 * (rectSize / 2),
            movementsXOffsets: [width /8, 0, width],
            movementsYOffsets: [0, -width / 16, 0],
        },
        // Right between main up and horizontal
        {
            startX: centerX + rectSize / 2,
            startY: centerY - 0.2 * (rectSize / 2),
            movementsXOffsets: [width /6, 0, width],
            movementsYOffsets: [0, -width / 30, 0],
        },
        // Horizontal right
        {
            startX: centerX + rectSize / 2,
            startY: centerY,
            movementsXOffsets: [width, 0, 0],
            movementsYOffsets: [0, - width / 15, 0],
        },
        // Right between main down and horizontal
        {
            startX: centerX + rectSize / 2,
            startY: centerY + 0.2 * (rectSize / 2),
            movementsXOffsets: [width /6, 0, width],
            movementsYOffsets: [0, width / 30, 0],
        },
        // Right between main up and horizontal
        {
            startX: centerX + rectSize / 2,
            startY: centerY + 0.4 * (rectSize / 2),
            movementsXOffsets: [width /8, 0, width],
            movementsYOffsets: [0, width / 20, 0],
        },
    ];

    const leftLines = rightLines.map(line => {
      return {
        startX: centerX - rectSize / 2, // start from left edge of rect
        startY: line.startY,             // same vertical positions
        movementsXOffsets: line.movementsXOffsets.map((offset, i) => {
          // flip direction: go left instead of right
          if (i === line.movementsXOffsets.length - 1) {
            // last step: reach left border
            return - (centerX - rectSize / 2) - (offset > 0 ? offset : 0);
          }
          return -offset;
        }),
        movementsYOffsets: line.movementsYOffsets, // same vertical wiggles
      };
    });

    const topLines = [
    // top center
      {
          startX: centerX,
          startY: centerY - rectSize / 2,
          movementsXOffsets: [0, 0, width],
          movementsYOffsets: [-width, 0, 0],
      },
      // Right
      {
          startX: centerX + rectSize / 3,
          startY: centerY - rectSize / 2,
          movementsXOffsets: [0, width / 15, 0, width / 2],
          movementsYOffsets: [-width / 30, 0, -width / 7, 0],
      },
      {
          startX: centerX + rectSize / 6,
          startY: centerY - rectSize / 2,
          movementsXOffsets: [0, width / 22, 0, width / 2],
          movementsYOffsets: [-width / 20, 0, -width / 3, 0],
      },
      // Left
      {
          startX: centerX - rectSize / 3,
          startY: centerY - rectSize / 2,
          movementsXOffsets: [0, -width / 15, 0, -width / 2],
          movementsYOffsets: [-width / 30, 0, -width / 7, 0],
      },
      {
          startX: centerX - rectSize / 6,
          startY: centerY - rectSize / 2,
          movementsXOffsets: [0, -width / 22, 0, -width / 2],
          movementsYOffsets: [-width / 20, 0, -width / 3, 0],
      },
    ]
  
    const bottomLines = topLines.map(line => {
      return {
        startX: line.startX, // same X positions
        startY: centerY + rectSize / 2, // reflected starting Y (bottom of rect)
        movementsXOffsets: [...line.movementsXOffsets], // same horizontal movements
        movementsYOffsets: line.movementsYOffsets.map(offset => -offset), // flip vertical direction
      };
    });

  const randomLines = [...rightLines, ...leftLines, ...topLines, ...bottomLines]
  return randomLines;
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


export function createMainLines(circuitLines, glow=false) {

    const svg = document.getElementById("circuitSvg");
    circuitLines.forEach(LineConfig => {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "path");
        let path = `M ${LineConfig.startX} ${LineConfig.startY} L ${LineConfig.startX + LineConfig.movementsXOffsets[0]} ${LineConfig.startY + LineConfig.movementsYOffsets[0]} `
        for(let i = 1; i < LineConfig.movementsXOffsets.length; i++) {
          path += `l ${LineConfig.movementsXOffsets[i]} ${LineConfig.movementsYOffsets[i]} `
        }
        line.setAttribute("d", path);
        // line.setAttribute("d", `M ${LineConfig.startX} ${LineConfig.startY} L ${LineConfig.startX + LineConfig.movementsXOffsets[0]} ${LineConfig.startY + LineConfig.movementsYOffsets[0]} l ${LineConfig.movementsXOffsets[1]} ${LineConfig.movementsYOffsets[1]} l ${LineConfig.movementsXOffsets[2]} ${LineConfig.movementsYOffsets[2]}`)
        line.setAttribute("stroke", "var(--primary)");
        line.setAttribute("stroke-width", "2");
        line.setAttribute("fill", "None");
        if (glow) {
          line.setAttribute("filter", "url(#glow)");
        }
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
      let circleXCenter = 0;

      // Create rectangle according to the window/svg size
      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", centerX - rectSize / 2);
      rect.setAttribute("y", centerY - rectSize / 2);
      rect.setAttribute("width", rectSize);
      rect.setAttribute("height", rectSize);
      rect.setAttribute("fill", "#00415a");
      rect.setAttribute("filter", "url(#glow)");
      svg.appendChild(rect);

      const M = document.createElementNS(SVG_NS, "path");
      M.setAttribute("d", `
        M ${centerX - rectSize * 0.3} ${centerY + rectSize * 0.3}
        V ${centerY - rectSize * 0.3}
        L ${centerX} ${centerY + rectSize * 0.2}
        L ${centerX + rectSize * 0.3} ${centerY - rectSize * 0.3}
        V ${centerY + rectSize * 0.3}
      `);
      M.setAttribute("stroke", "var(--primary)");
      M.setAttribute("stroke-width", "3");
      M.setAttribute("fill", "none");
      M.setAttribute("filter", "url(#glow)");
      svg.appendChild(M);

      const compCircuitLines = generateComlementaryLines();
      // Create main lines
      createMainLines(mainCircutLines, true);

      createMainLines(compCircuitLines, false);

      subSystems.forEach((val, i) => {
        const LineConfig = mainCircutLines[i];
        const endX = LineConfig.startX + LineConfig.movementsXOffsets[0] + LineConfig.movementsXOffsets[1] + LineConfig.movementsXOffsets[2];
        const endY = LineConfig.startY + LineConfig.movementsYOffsets[0] + LineConfig.movementsYOffsets[1] + LineConfig.movementsYOffsets[2];
        console.log(`SUBSYSTEM ${i}`)
        console.log(`endX : ${endX}`)
        console.log(`endY : ${endY}`)
        
        if (endX < width/2) {
          circleXCenter = endX - 0.04 * rectSize;
          subSystems[i].position = {x : endX - 0.1 * rectSize, y : endY - Math.abs(LineConfig.movementsYOffsets[1]) / 2};
        } else{
          circleXCenter = endX + 0.04 * rectSize;
          subSystems[i].position = {x : endX + 0.1 * rectSize, y : endY - Math.abs(LineConfig.movementsYOffsets[1]) / 2};
        }

        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", circleXCenter);
        circle.setAttribute("cy", endY);
        circle.setAttribute("r", 8);   // radius
        circle.setAttribute("fill", "none");  // keep center transparent
        circle.setAttribute("stroke", "var(--primary)");
        circle.setAttribute("stroke-width", "2");
        svg.appendChild(circle);
      });

      
      // Create vision systems div
      createSubSystems(subSystems, width);

    }
     