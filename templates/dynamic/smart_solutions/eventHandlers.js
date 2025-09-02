export function subsystemListOnHoverEvent(e, videoContainerElement, elementsList) {
      const link = e.target.closest('a');
      const sourceElement = videoContainerElement.querySelector('source');
      const videoElement = videoContainerElement.querySelector('video'); 

      if (!link || !elementsList.contains(link))
      {
        videoElement.pause();
        return;
      } 

      const newSrc = link.getAttribute('data-video');
      if (sourceElement.getAttribute('src') !== newSrc) {
        sourceElement.setAttribute('src', newSrc);
        videoElement.load();
      }
      videoElement.style.opacity = 0.7;
      videoElement.parentElement.style.backgroundImage = 'none';
      videoElement.play();
    }

export function subsystemListOnMouseLeave(videoContainerElement, defaultVideoSrc, backgroundImage) {
    const sourceElement = videoContainerElement.querySelector('source');
    const videoElement = videoContainerElement.querySelector('video');

    sourceElement.setAttribute('src', defaultVideoSrc);
    videoElement.load();
    videoElement.pause();
    videoElement.style.opacity = 0;
    videoElement.parentElement.style.backgroundImage = `url(${backgroundImage})`;
}