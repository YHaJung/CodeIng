import {
  Component,
  OnInit,
  Input,
  EventEmitter,
  ViewChild,
  TemplateRef,
  ContentChild,
} from '@angular/core';
import { TabLabelComponent } from './tab-label.component';
import { TabBodyComponent } from './tab-body.component';

@Component({
  selector: 'app-tab-item',
  template: '<ng-content></ng-content>',
})
export class TabItemComponent implements OnInit {
  @Input()
  label: string;

  @Input()
  isActive: boolean;

  @ContentChild(TabBodyComponent)
  bodyComponent: TabBodyComponent;

  @ContentChild(TabLabelComponent)
  labelComponent: TabLabelComponent;

  constructor() {}

  ngOnInit(): void {}
}
