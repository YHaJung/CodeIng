import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureRecommendComponent } from './lecture-recommend.component';

describe('LectureRecommendComponent', () => {
  let component: LectureRecommendComponent;
  let fixture: ComponentFixture<LectureRecommendComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureRecommendComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureRecommendComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
