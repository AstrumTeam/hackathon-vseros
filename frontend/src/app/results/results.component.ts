import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Clip, MainService, ServerResponse } from '../services/main-service.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit{

  loading: boolean = false;

  clips: Clip[] = [];

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private service: MainService,
  ){}

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
      console.log(this.clips);  // вывод первого элемента в консоль
    });
  }

  again(){
    this.router.navigate([``]);
  }

  ngOnInit(): void {
    // console.log('начало', this.clips)
    // if(this.clips === null){
    //   this.route.queryParams.subscribe(params => {
    //     if (params['clips']) {
    //       // Используем JSON.parse для преобразования строки обратно в массив
    //       this.clips = JSON.parse(params['clips']);
    //       console.log(this.clips); // Теперь вы получите массив строк
    //       console.log(this.clips[0])
    //       this.loading = false;
    //     }
    //   });
    // }
    // else{
    //   console.log(this.clips)
    //   this.loading = false;
    // }


    this.clips = this.service.clips;
    console.log(this.clips);
    //console.log('results',this.clips, typeof(this.service.clips))
  }
}
