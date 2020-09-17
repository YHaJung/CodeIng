import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureRecommendDetailComponent } from './lecture-recommend-detail.component';

describe('LectureRecommendDetailComponent', () => {
  let component: LectureRecommendDetailComponent;
  let fixture: ComponentFixture<LectureRecommendDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureRecommendDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureRecommendDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
