// script.js

document.addEventListener("DOMContentLoaded", function () {
    let track = document.querySelector(".carousel-track");
    let images = document.querySelectorAll(".carousel-track img");

    let index = 0;
    let imageWidth = images[0].clientWidth;
    let totalImages = images.length;

    function moveCarousel() {
        index++;
        if (index >= totalImages) {
            index = 0;
        }
        track.style.transform = `translateX(${-index * imageWidth}px)`;
    }
    // Move every 2 seconds
    setInterval(moveCarousel, 2000);
});

document.addEventListener("DOMContentLoaded", () => {
  const elements = document.querySelectorAll(".power");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
      } else {
        entry.target.classList.remove("show"); // remove this line if you want animation only once
      }
    });
  }, { threshold: 0.2 }); // 20% of the section must be visible

  elements.forEach(el => observer.observe(el));
});





document.addEventListener("DOMContentLoaded", () => {
  const elements = document.querySelectorAll(".animate-on-scroll");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
      } else {
        entry.target.classList.remove("show"); // remove this line if you want animation only once
      }
    });
  }, { threshold: 0.2 }); // 20% of the section must be visible

  elements.forEach(el => observer.observe(el));
});



// for static background..
document.addEventListener("DOMContentLoaded", () => {
  const parallaxItems = document.querySelectorAll(".parallax-effect");

  // Set up observer
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // Start scroll listener for this element
        window.addEventListener("scroll", () => {
          const speed = parseFloat(entry.target.dataset.speed) || 0.5;
          const yPos = window.scrollY * speed;
          entry.target.style.transform = `translateY(${yPos}px)`;
        });
      }
    });
  }, { threshold: 0 }); // Trigger as soon as any part is visible

  parallaxItems.forEach(el => observer.observe(el));
});
