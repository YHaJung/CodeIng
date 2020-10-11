import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureQnaComponent } from './lecture-qna.component';

describe('LectureQnaComponent', () => {
  let component: LectureQnaComponent;
  let fixture: ComponentFixture<LectureQnaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureQnaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureQnaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
