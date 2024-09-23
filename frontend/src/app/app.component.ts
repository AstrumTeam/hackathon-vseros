import { Component } from '@angular/core';
import { MainService } from './services/main-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  showResult = false;

  showSettings = false;

  isActiveSubtitles: boolean = false;

  showSizes = false;

  modelSizes = ['tiny', 'base', 'small', 'medium',' large', 'large-v1', 'large-v2', 'large-v3'];

  modelSizesSelected = 'Размер используемой модели';

  title = 'Astrum';

  constructor(
    private service: MainService,
  ){}

  modelSizeSelected(size: string){
    this.modelSizesSelected = size;
    this.showSizes = false;
  }

  showSizesEvent(){
    this.showSizes = !this.showSizes;
  }


  toggleSubtitles(): void {
    this.isActiveSubtitles = !this.isActiveSubtitles;
  }

  upload(){
    this.showResult = !this.showResult;
    this.showSettings = !this.showSettings;
  }

  settings(){
    this.showSettings = !this.showSettings;
  }

  again(){
    this.showResult = false;
    this.showSettings = false;
  }
}
