import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { LectureQnaCommentsComponent } from './lecture-qna-comments.component';

describe('LectureQnaCommentsComponent', () => {
  let component: LectureQnaCommentsComponent;
  let fixture: ComponentFixture<LectureQnaCommentsComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureQnaCommentsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureQnaCommentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
