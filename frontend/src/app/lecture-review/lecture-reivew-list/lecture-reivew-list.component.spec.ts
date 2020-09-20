import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureReivewListComponent } from './lecture-reivew-list.component';

describe('LectureReivewListComponent', () => {
  let component: LectureReivewListComponent;
  let fixture: ComponentFixture<LectureReivewListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureReivewListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureReivewListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
