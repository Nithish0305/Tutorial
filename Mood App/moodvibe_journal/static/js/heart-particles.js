class HeartParticles {
    constructor() {
        this.hearts = [];
        this.isActive = false;
        this.maxHearts = 20;
    }

    start() {
        if (this.isActive) return;
        this.isActive = true;
        this.createHearts();
    }

    stop() {
        this.isActive = false;
        this.hearts.forEach(heart => {
            if (heart.element && heart.element.parentNode) {
                heart.element.parentNode.removeChild(heart.element);
            }
        });
        this.hearts = [];
    }

    createHearts() {
        if (!this.isActive) return;

        if (this.hearts.length < this.maxHearts) {
            const heart = document.createElement('div');
            heart.className = 'heart-particle';
            heart.innerHTML = '❤';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.animationDuration = (Math.random() * 3 + 2) + 's';
            heart.style.fontSize = (Math.random() * 20 + 10) + 'px';
            document.body.appendChild(heart);

            const heartObj = {
                element: heart,
                timeCreated: Date.now()
            };

            this.hearts.push(heartObj);

            heart.addEventListener('animationend', () => {
                if (heart.parentNode) {
                    heart.parentNode.removeChild(heart);
                }
                this.hearts = this.hearts.filter(h => h !== heartObj);
            });
        }

        if (this.isActive) {
            requestAnimationFrame(() => this.createHearts());
        }
    }
}

// Initialize heart particles
const heartParticles = new HeartParticles();