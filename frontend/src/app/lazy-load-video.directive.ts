import { Directive, ElementRef, Input, OnInit } from '@angular/core';

@Directive({
  selector: '[appLazyLoadVideo]'
})
export class LazyLoadVideoDirective implements OnInit {

  @Input() src: string = '';  // URL видео, который будет лениво загружаться

  constructor(private el: ElementRef) { }

  ngOnInit(): void {
    // Проверяем, поддерживает ли браузер IntersectionObserver
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.loadVideo();  // Загружаем видео, если оно попало в область видимости
            observer.unobserve(this.el.nativeElement);  // Отключаем наблюдение
          }
        });
      });

      observer.observe(this.el.nativeElement);  // Начинаем наблюдение за элементом
    } else {
      // Если IntersectionObserver не поддерживается, загружаем видео сразу
      this.loadVideo();
    }
  }

  private loadVideo(): void {
    const videoElement: HTMLVideoElement = this.el.nativeElement;
    const source = document.createElement('source');
    source.src = this.src;
    videoElement.appendChild(source);
    videoElement.load();  // Загружаем видео
  }
}