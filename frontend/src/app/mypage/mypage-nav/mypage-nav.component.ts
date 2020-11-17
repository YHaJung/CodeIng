import { Component, Input, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-mypage-nav',
  templateUrl: './mypage-nav.component.html',
  styleUrls: ['./mypage-nav.component.css']
})
export class MypageNavComponent implements OnInit {
  @Input() key: number;
  
  mypagekey = 0;
  constructor(private route: ActivatedRoute ) { }
  
  ngOnInit(): void {
    this.mypagekey = this.key;
  }

}
