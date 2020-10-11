import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureSearchComponent } from './lecture-search.component';

describe('LectureSearchComponent', () => {
  let component: LectureSearchComponent;
  let fixture: ComponentFixture<LectureSearchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LectureSearchComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
