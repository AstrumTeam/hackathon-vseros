import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

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

  clips: string[] = [];

  constructor(
    private httpClient: HttpClient,
  ) { }

  private baseUrl = 'https://8d0c-83-220-236-222.ngrok-free.app';

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

  }
}
