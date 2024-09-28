import { Component } from '@angular/core';
import { MainService, Video } from '../services/main-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent {
  threshold: number = 0.50;

  clips: string[] = [];

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

  startGeneration(){
    this.service.generate(this.video);
  }

  isVideoUploaded: boolean = false;

  isDragOver: boolean = false;

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];

      this.uploadVideo(file);
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

  upload(){
    this.showSettings = !this.showSettings;
    this.service.addVideo(this.video).subscribe((data: any) => {
      console.log('ОТВЕТ СЕРВЕРА',data)
      this.clips = data;
      this.router.navigate([`/results`], { queryParams: { clips: JSON.stringify(this.clips) } });
    });

    this.startGeneration();
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
