import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { LectureQnaComponent } from './lecture-qna.component';

describe('LectureQnaComponent', () => {
  let component: LectureQnaComponent;
  let fixture: ComponentFixture<LectureQnaComponent>;

  beforeEach(waitForAsync(() => {
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
