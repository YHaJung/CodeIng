import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WriteLectureQnaComponent } from './write-lecture-qna.component';

describe('WriteLectureQnaComponent', () => {
  let component: WriteLectureQnaComponent;
  let fixture: ComponentFixture<WriteLectureQnaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WriteLectureQnaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WriteLectureQnaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
