import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureReviewNavBarComponent } from './lecture-review-nav-bar.component';

describe('LectureReviewNavBarComponent', () => {
  let component: LectureReviewNavBarComponent;
  let fixture: ComponentFixture<LectureReviewNavBarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureReviewNavBarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureReviewNavBarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
