import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import JSZip from 'jszip';

export interface Video{
  subtitles: boolean,
  fields: boolean,
  face_tracking: boolean,
  humor: boolean,
  clickbait: boolean,
  threshold: number,
  min_length: number,
  max_length: number,
  video: File | null
}

export interface ServerResponse{
  clips: string[];
}

@Injectable({
  providedIn: 'root'
})
export class MainService {
  videos: Blob[] = [];

  constructor(
    private httpClient: HttpClient,
  ) { }

  private baseUrl = 'https://19e7-83-220-236-131.ngrok-free.app';

  downloadAndExtract() {
    this.downloadVideos().subscribe((zipBlob: Blob) => {
      const zipReader = new JSZip();

      // Загружаем ZIP-файл в JSZip
      zipReader.loadAsync(zipBlob).then((zip) => {
        // Явно указываем тип для videoPromises
        const videoPromises: Promise<Blob>[] = [];

        // Проходим по всем файлам в ZIP-архиве
        zip.forEach((relativePath, zipEntry) => {
          // Проверяем, является ли файл видео
          if (zipEntry.name.endsWith('.mp4')) {
            const videoPromise = zipEntry.async('blob').then((blob) => {
              // Возвращаем blob-объект для видео
              return blob; // Возвращаем Blob для видео
            });
            videoPromises.push(videoPromise);
          }
        });

        // Ждем, пока все видео будут распакованы
        Promise.all(videoPromises).then((videoBlobs) => {
          this.videos = videoBlobs; // Записываем Blob-объекты в массив
          console.log('Video files:', this.videos); // Выводим в консоль
        });
      });
    });
  }

  addVideo(videoData: Video): Observable<ServerResponse> {
    const formData = new FormData();

    formData.append('subtitles', videoData.subtitles.toString());
    formData.append('fields', videoData.fields.toString());
    formData.append('face_tracking', videoData.face_tracking.toString());
    formData.append('humor', videoData.humor.toString());
    formData.append('clickbait', videoData.clickbait.toString());
    formData.append('threshold', videoData.threshold.toString());
    formData.append('min_length', videoData.min_length.toString());
    formData.append('max_length', videoData.max_length.toString());

    if (videoData.video) {
        formData.append('video', videoData.video);
    }

    formData.forEach((value, key) => {
      console.log(key, value);
    });

    return this.httpClient.post<ServerResponse>(this.baseUrl + "/api/create/clips", formData);
  }

  downloadVideos(): Observable<Blob> {
    return this.httpClient.get(`${this.baseUrl}/download_videos`, { responseType: 'blob' });
  }

  generate(data: Video){
    console.log(data)
  }
}
