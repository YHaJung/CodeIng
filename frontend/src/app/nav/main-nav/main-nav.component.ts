import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-main-nav',
  templateUrl: './main-nav.component.html',
  styleUrls: ['./main-nav.component.css']
})
export class MainNavComponent implements OnInit {
  @Input() tab : string;

  constructor() { }

  ngOnInit(): void {
    console.log('tab');
    console.log(this.tab);
  }

}
