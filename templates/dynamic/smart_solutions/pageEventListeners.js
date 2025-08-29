export function updateScrollLineGradient() {
    const scrollLine = document.getElementById('subsoln-scroll-line');
    const viewportHeight = window.innerHeight;
    const scrollTop = window.scrollY;
    const lineTop = scrollLine.getBoundingClientRect().top + scrollTop;
    const lineHeight = scrollLine.offsetHeight;
    const dots = document.querySelectorAll('.sub-soln-dot');
    // Compute the center of the screen relative to the scroll line
    const centerY = scrollTop + viewportHeight / 2;
    const relativeCenter = (centerY - lineTop) / lineHeight;

    // Clamp values to prevent invalid percentages
    const focusStart = Math.max(0, relativeCenter - 0.1);
    const focusEnd = Math.min(1, relativeCenter + 0.1);

    // Convert to percentages
    const start = (focusStart * 100).toFixed(2);
    const mid = (relativeCenter * 100).toFixed(2);
    const end = (focusEnd * 100).toFixed(2);

    const center = window.innerHeight / 2; // Middle of viewport
    const range = 20; // Sensitivity range (px)

    // Set dynamic gradient
    scrollLine.style.background = `linear-gradient(
      to bottom,
      rgba(0, 113, 156, 0.2) 0%,
      rgba(0, 113, 156, 0.4) ${start}%,
      #0ff ${mid}%,
      rgba(0, 113, 156, 0.4) ${end}%,
      rgba(0, 113, 156, 0.2) 100%
    )`;

    for(const dot of dots) {
      const dotPosition = dot.getBoundingClientRect().top;
      const circle = dot.querySelector('circle'); // <- this is key
      if (dotPosition > (centerY - range) && dotPosition < (centerY + range)) {
        dot.style.fill = "#0FF"; // In-focus color
      } else {
        dot.style.fill = "#00719c"; // Dimmed color
      }
    }
  }

export function scrollCardsRight() {
    const subSectionContainer = document.querySelector('.sub-solutions-container');
    subSectionContainer.scrollBy({left:300, behavior: "smooth"})
  }

export function scrollCardsLeft() {
    const subSectionContainer = document.querySelector('.sub-solutions-container');
    subSectionContainer.scrollBy({left:-300, behavior: "smooth"})
  }