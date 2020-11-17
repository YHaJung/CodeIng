import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-mypage-specific',
  templateUrl: './mypage-specific.component.html',
  styleUrls: ['./mypage-specific.component.css']
})
export class MypageSpecificComponent implements OnInit {

  constructor(private route: ActivatedRoute ) { }
  mypagekey = 0;
  ngOnInit(): void {
    this.mypagekey = +this.route.snapshot.paramMap.get('mypagekey');
  }

}
