import { Component } from '@angular/core';
import { Clip, MainService, ServerResponse, Video } from '../services/main-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent {
  threshold: number = 0.50;

  clips: Clip[] = [];

  loading: boolean = false;

  video: Video = {
    subtitles: false,
    fields: false,
    face_tracking: false,
    humor: false,
    clickbait: false,
    threshold: 0.50,
    min_length: 10,
    max_length: 90,
    video: null
  }

  showSettings = false;

  showSizes = false;

  modelSizes = ['base', 'small', 'medium',' large', 'large-v1', 'large-v2', 'large-v3'];

  modelSizesSelected = 'large-v3';

  title = 'Astrum';

  constructor(
    private service: MainService,
    private router: Router,
  ){}

  isVideoUploaded: boolean = false;

  isDragOver: boolean = false;

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
        const file = input.files[0];

        // Создаем URL объекта для видеофайла
        const videoURL = URL.createObjectURL(file);
        const video = document.createElement('video');

        // Загружаем метаданные видео
        video.preload = 'metadata';
        video.onloadedmetadata = () => {
            const duration = video.duration; // Длительность в секундах

            // Проверяем условия длительности
            if (duration < 60 || duration > 7200) { // 60 секунд = 1 минута, 7200 секунд = 2 часа
                alert('Длительность видео должна быть от 1 минуты до 2 часов.');
                return;
            }

            // Если длительность подходит, продолжаем загрузку
            this.uploadVideo(file);
        };

        // Начинаем загрузку метаданных
        video.src = videoURL;
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver = false;

    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
      const file = event.dataTransfer.files[0];

      this.uploadVideo(file);
    }
  }

  uploadVideo(file: File): void {
    this.video.video = file;
    console.log('Загруженное видео:', this.video.video);
    this.isVideoUploaded = true;

    setTimeout(() => {
      this.settings();
    }, 1000)
  }

  modelSizeSelected(size: string){
    this.modelSizesSelected = size;
    this.showSizes = false;
  }

  showSizesEvent(){
    this.showSizes = !this.showSizes;
  }

  togglerFields(){
    this.video.fields = !this.video.fields;
  }

  toggleSubtitles(): void {
    this.video.subtitles = !this.video.subtitles;
  }

  toggleHumor(): void {
    this.video.humor = !this.video.humor;
  }

  toggleClickbait(): void {
    this.video.clickbait = !this.video.clickbait;
  }

  toggleFace(): void {
    this.video.face_tracking = !this.video.face_tracking;
  }

  getTest() {
    this.service.getTest().subscribe((data: ServerResponse) => {
      // Преобразуем массив массивов в массив объектов Clip
      const clipsArray: Clip[] = data.clips.map(clip => ({
        id: clip[0],
        tag: clip[1],
        rate: clip[2]
      }));
  
      this.clips = clipsArray;
  
      // Теперь `this.clips` содержит массив объектов с типом `Clip`
      console.log(this.clips[0]);  // вывод первого элемента в консоль
    });
  }

  upload(){
    this.showSettings = !this.showSettings;
    this.loading = true;
    this.service.addVideo(this.video).subscribe((data: ServerResponse) => {
      // Преобразуем массив массивов в массив объектов Clip
      const clipsArray: Clip[] = data.clips.map(clip => ({
        id: clip[0],
        tag: clip[1],
        rate: clip[2]
      }));
  
      this.clips = clipsArray;
      this.service.clips = clipsArray;
      this.router.navigate([`/results`]);
    });
  }

  settings(){
    this.showSettings = !this.showSettings;
  }

  again(){
    this.showSettings = false;

    this.video = {
      subtitles: false,
      fields: false,
      face_tracking: false,
      humor: false,
      clickbait: false,
      threshold: 0.5,
      min_length: 10,
      max_length: 90,
      video: null
    }
  }
}
