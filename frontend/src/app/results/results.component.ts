import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MainService } from '../services/main-service.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit{

  loading: boolean = false;

  clips: string[] = [];

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private service: MainService,
  ){}
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
  }

  again(){
    this.router.navigate([``]);
  }
}
