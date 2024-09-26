import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Video{
  subtitles: boolean,
  phone_format: boolean,
  face_tracking: boolean,
  video: File | null
}

export interface ServerResponse{
  success: boolean;
  message: string;
  data: any;
}

@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor() { }

  generate(data: Video){
    console.log(data)
  }
}
