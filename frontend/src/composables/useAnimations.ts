/**
 * ✨ useAnimations - Composable for triggering animations
 * MatrixCalc v3.0
 */

import { ref, computed } from 'vue';

export type AnimationType = 
  | 'shake' 
  | 'pulse' 
  | 'bounce' 
  | 'wiggle' 
  | 'matrix-flip' 
  | 'wave'
  | 'number-pop'
  | 'ripple-effect';

export interface AnimationOptions {
  duration?: number;
  delay?: number;
  onComplete?: () => void;
}

export function useAnimations() {
  const activeAnimations = ref<Map<string, boolean>>(new Map());

  /**
   * Trigger an animation on an element
   */
  const animate = (
    elementId: string,
    animation: AnimationType,
    options: AnimationOptions = {}
  ) => {
    const { duration = 600, delay = 0, onComplete } = options;

    if (delay > 0) {
      setTimeout(() => applyAnimation(elementId, animation, duration, onComplete), delay);
    } else {
      applyAnimation(elementId, animation, duration, onComplete);
    }
  };

  const applyAnimation = (
    elementId: string,
    animation: AnimationType,
    duration: number,
    onComplete?: () => void
  ) => {
    activeAnimations.value.set(elementId, true);

    const element = document.getElementById(elementId);
    if (!element) {
      console.warn(`Element with id "${elementId}" not found`);
      return;
    }

    element.classList.add(animation);

    setTimeout(() => {
      element.classList.remove(animation);
      activeAnimations.value.delete(elementId);
      onComplete?.();
    }, duration);
  };

  /**
   * Shake animation - typically for errors
   */
  const shake = (elementId: string) => {
    animate(elementId, 'shake', { duration: 500 });
  };

  /**
   * Pulse animation - for highlighting
   */
  const pulse = (elementId: string, duration: number = 2000) => {
    animate(elementId, 'pulse', { duration });
  };

  /**
   * Matrix flip animation - for template changes
   */
  const matrixFlip = (elementId: string, onComplete?: () => void) => {
    animate(elementId, 'matrix-flip', { duration: 600, onComplete });
  };

  /**
   * Number pop animation - for new values
   */
  const numberPop = (elementId: string) => {
    animate(elementId, 'number-pop', { duration: 400 });
  };

  /**
   * Wave animation - for success
   */
  const wave = (elementId: string) => {
    animate(elementId, 'wave', { duration: 1000 });
  };

  /**
   * Create confetti effect
   */
  const confetti = (count: number = 50) => {
    const colors = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
      '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'
    ];

    for (let i = 0; i < count; i++) {
      setTimeout(() => {
        const particle = document.createElement('div');
        particle.className = 'confetti-particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)] || '#FF6B6B';
        particle.style.animationDelay = Math.random() * 0.5 + 's';
        
        document.body.appendChild(particle);

        setTimeout(() => {
          particle.remove();
        }, 3000);
      }, i * 30);
    }
  };

  /**
   * Stagger animation for multiple elements
   */
  const staggerAnimation = (
    elementIds: string[],
    animation: AnimationType,
    delayBetween: number = 100
  ) => {
    elementIds.forEach((id, index) => {
      animate(id, animation, { delay: index * delayBetween });
    });
  };

  /**
   * Ripple effect on click
   */
  const createRipple = (event: MouseEvent) => {
    const button = event.currentTarget as HTMLElement;
    const ripple = document.createElement('span');
    
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');

    const existingRipple = button.querySelector('.ripple');
    if (existingRipple) {
      existingRipple.remove();
    }

    button.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 600);
  };

  /**
   * Check if an element is currently animating
   */
  const isAnimating = (elementId: string): boolean => {
    return activeAnimations.value.get(elementId) ?? false;
  };

  return {
    animate,
    shake,
    pulse,
    matrixFlip,
    numberPop,
    wave,
    confetti,
    staggerAnimation,
    createRipple,
    isAnimating,
    activeAnimations: computed(() => activeAnimations.value)
  };
}

/**
 * Helper styles for ripple effect
 * Add this CSS to your component or global styles:
 * 
 * .ripple {
 *   position: absolute;
 *   border-radius: 50%;
 *   background: rgba(255, 255, 255, 0.6);
 *   transform: scale(0);
 *   animation: ripple-animation 0.6s ease-out;
 *   pointer-events: none;
 * }
 * 
 * @keyframes ripple-animation {
 *   to {
 *     transform: scale(2.5);
 *     opacity: 0;
 *   }
 * }
 */
