#!/usr/bin/env python3
"""
Script to train ML models for career recommendation system
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.ml.train_model import train_models

if __name__ == "__main__":
    print("Starting model training...")
    print("=" * 60)
    train_models()
    print("=" * 60)
    print("Training complete!")
