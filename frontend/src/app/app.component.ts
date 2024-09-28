import { Component } from '@angular/core';
import { MainService, Video } from './services/main-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // video: Video = {
  //   subtitles: false,
  //   phone_format: false,
  //   face_tracking: false,
  //   video: null
  // }

  // showResult = false;

  // showSettings = false;

  // showSizes = false;

  // modelSizes = ['tiny', 'base', 'small', 'medium',' large', 'large-v1', 'large-v2', 'large-v3'];

  // modelSizesSelected = 'Размер используемой модели';

  // title = 'Astrum';

  // constructor(
  //   private service: MainService,
  // ){}

  // startGeneration(){
  //   this.service.generate(this.video);
  // }

  // isVideoUploaded: boolean = false; // Переменная для отслеживания состояния загрузки

  // onFileSelected(event: Event): void {
  //   const input = event.target as HTMLInputElement;
  //   if (input.files && input.files.length > 0) {
  //     const file = input.files[0];

  //     this.video.video = file;
  //     console.log('Выбранное видео:', this.video.video);
  //     this.isVideoUploaded = true;
  //   }
  // }

  // modelSizeSelected(size: string){
  //   this.modelSizesSelected = size;
  //   this.showSizes = false;
  // }

  // showSizesEvent(){
  //   this.showSizes = !this.showSizes;
  // }


  // toggleSubtitles(): void {
  //   this.video.subtitles = !this.video.subtitles;
  // }

  // togglePhone(): void {
  //   this.video.phone_format = !this.video.phone_format;
  //   if(!this.video.phone_format){
  //     this.video.face_tracking = false;
  //   }
  // }

  // toggleFace(): void {
  //   this.video.face_tracking = !this.video.face_tracking;
  // }

  // upload(){
  //   this.showResult = !this.showResult;
  //   this.showSettings = !this.showSettings;
  //   this.startGeneration();
  // }

  // settings(){
  //   this.showSettings = !this.showSettings;
  // }

  // again(){
  //   this.showResult = false;
  //   this.showSettings = false;

  //   this.video = {
  //     subtitles: false,
  //     phone_format: false,
  //     face_tracking: false,
  //     video: null
  //   }
  // }
}
