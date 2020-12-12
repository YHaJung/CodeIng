import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { LectureReviewComponent } from './lecture-review.component';

describe('LectureReviewComponent', () => {
  let component: LectureReviewComponent;
  let fixture: ComponentFixture<LectureReviewComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureReviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureReviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
