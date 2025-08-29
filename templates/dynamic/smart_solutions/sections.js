import { subSystems, SOLNLIMIT, SOLNINITIALOFFSET } from './config.js';
import { getSolutionData} from './routes.js';

// Builds each solution card
function createSolution(solutionData) {
    const solnCard = document.createElement('div');
    solnCard.className = "soln-card";

    // Shorts
    const shorts = document.createElement('div');
    shorts.className = "soln-card-shorts";

    const link = document.createElement('a');
    link.href = solutionData.url || "#";
    link.target = "_blank";
    link.className = "soln-link";

    const img = document.createElement('img');
    img.src = solutionData.images.url;
    img.alt = solutionData.images.alt || "Solution Image";

    link.appendChild(img);
    shorts.appendChild(link);

    // Add switch buttons
    const videoBtn = document.createElement('button');
    videoBtn.className = "video-switch-btn soln-card-btn";

    const imgBtn = document.createElement('button');
    imgBtn.className = "img-switch-btn soln-card-btn";

    shorts.appendChild(videoBtn);
    shorts.appendChild(imgBtn);

    // Content
    const content = document.createElement('div');
    content.className = "soln-content";

    const contentLink = document.createElement('a');
    contentLink.href = solutionData.url || "#";
    contentLink.target = "_blank";
    contentLink.className = "soln-link";

    const nameDiv = document.createElement('div');
    nameDiv.className = "soln-name";
    nameDiv.innerText = solutionData.name;

    contentLink.appendChild(nameDiv);
    console.log("solutionData : ", solutionData)
    const ownerDiv = document.createElement('div');
    ownerDiv.className = "soln-owner";
    ownerDiv.innerText = `by ${solutionData.owner}`;

    const iconContainer = document.createElement('div');
    iconContainer.className = "icon-container";

    const dropdown = document.createElement('ul');
    dropdown.className = "icon-dropdown";
    dropdown.innerHTML = `
        <li>Source Code</li>
        <li>Executable</li>
    `;

    iconContainer.appendChild(dropdown);

    content.appendChild(contentLink);
    content.appendChild(ownerDiv);
    content.appendChild(iconContainer);

    solnCard.appendChild(shorts);
    solnCard.appendChild(content);

    return solnCard;
}

// Builds each sub-element (header + scroll buttons + solutions container)
function createSubElementContainer(element) {
    const container = document.createElement("div");
    container.className = "sub-solution";

    // Header
    const header = document.createElement("div");
    header.className = "sub-solution-header";
    header.innerText = element.name
        .replace(/-/g, " ")
        .replace(/\b\w/g, c => c.toUpperCase());

    // Scroll buttons
    const leftBtn = document.createElement("button");
    leftBtn.className = "scroll-btn left";
    leftBtn.setAttribute("onclick", "scrollCardsLeft()");
    leftBtn.innerHTML = "&#10094;";

    const rightBtn = document.createElement("button");
    rightBtn.className = "scroll-btn right";
    rightBtn.setAttribute("onclick", "scrollCardsRight()");
    rightBtn.innerHTML = "&#10095;";

    // Solutions container
    const solnsContainer = document.createElement("div");
    solnsContainer.className = "sub-solutions-container";

    // Fetch and append solutions
    getSolutionData('/solutions/solution', {
        offset: 0,
        limit: 10,
        category: element.link
    }).then(solutions => {
        solutions.forEach(soln => solnsContainer.appendChild(createSolution(soln)));
    });

    // Build final structure
    container.appendChild(header);
    container.appendChild(leftBtn);
    container.appendChild(solnsContainer);
    container.appendChild(rightBtn);

    return container;
}


export function createSystemsSections(mainContainer) {
    console.log(mainContainer);

    const subsystem = document.createElement("div");
    subsystem.className = "solution-section";

    // Section Header (capitalize words, replace "-")
    const subSolutionHeader = document.createElement("div");
    let subSolutionName = subSystems[0].name;
    subSolutionName = subSolutionName
        .replace(/-/g, " ")
        .replace(/\b\w/g, c => c.toUpperCase());
    subSolutionHeader.innerText = subSolutionName;
    subSolutionHeader.className = "section-header";

    subsystem.appendChild(subSolutionHeader);

    subSystems[0].subElements.forEach(sub => {
        subsystem.appendChild(createSubElementContainer(sub));
    })

    subsystem.id = subSystems[0].name;
    mainContainer.appendChild(subsystem);
}